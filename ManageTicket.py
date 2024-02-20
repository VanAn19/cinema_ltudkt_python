from Ticket import Ticket
from datetime import datetime, timedelta
from connect import cursor, conn
import pyodbc

class ManageTicket:
    def sellTicket(self, ticket):
        try:
            cursor.execute("SELECT COUNT(*) FROM Tickets WHERE room = ? AND showTime = ? AND seatPosition = ?", (ticket.room, ticket.showTime, ticket.seatPosition))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"Chỗ ngồi {ticket.seatPosition} trong phòng chiếu {ticket.room} đã được bán.")
                return

            cursor.execute("SELECT COUNT(*) FROM Tickets WHERE room = ? AND showTime = ?", (ticket.room, ticket.showTime))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"Phòng chiếu {ticket.room} đã có phim khác chiếu cùng một lúc.")
                return

            cursor.execute("SELECT ticketId FROM Tickets WHERE ticketId = ?", ticket.ticketId)
            existingTicket = cursor.fetchone()
            
            if existingTicket:
                print(f"Vé có mã {ticket.ticketId} đã được bán trước đó.")
            elif not ticket.ticketId.isdigit() or len(ticket.ticketId) != 4:
                print("Mã vé phải là số và có độ dài là 4 kí tự.")
            else:
                cursor.execute("INSERT INTO Tickets (ticketId, room, movieName, showTime, seatPosition, ticketType, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (ticket.ticketId, ticket.room, ticket.movieName, ticket.showTime, ticket.seatPosition, ticket.ticketType, ticket.price))
                conn.commit()
                print(f'Đã bán vé {ticket.ticketId}')
        except pyodbc.Error as e:
            conn.rollback()
            print(e)
    def cancelTicket(self, ticketId):
        try:
            cursor.execute("SELECT showTime, price FROM Tickets WHERE ticketId = ?", (ticketId,))
            row = cursor.fetchone()
            if row:
                showTime, price = row[0], row[1] 
                if self.isCancelAllowed(showTime):
                    refundAmount = 0.8 * price
                    cursor.execute("DELETE FROM Tickets WHERE ticketId = ?", (ticketId,))
                    conn.commit()
                    print(f"Đã hủy vé {ticketId} và hoàn tiền {refundAmount} VND.")
                else:
                    cursor.execute("DELETE FROM Tickets WHERE ticketId = ?", (ticketId,))
                    conn.commit()
                    print(f'Không thể hoàn tiền cho vé {ticketId} sau khi hủy.')
            else:
                print(f'Không tìm thấy vé có mã: {ticketId}.')
        except pyodbc.Error as e:
            conn.rollback()
            print(e)

    def isCancelAllowed(self, showTime):
        # currentTime = datetime.now()
        # showTime = datetime.strptime(ticket.showTime, '%Y-%m-%d %H:%M')
        # cancelTime = showTime - timedelta(hours=4) if (ticket.showTime <= "18:00") and (ticket.showTime >= "22:00") else showTime - timedelta(hours=6)
        # return currentTime <= cancelTime
        currentTime = datetime.now()
        cancelTime = showTime - timedelta(hours=4) if (showTime.hour <= 18) and (showTime >= "22:00") else showTime - timedelta(hours=6)
        return currentTime <= cancelTime
    def countTicketsByType(self):
        try:
            cursor.execute("SELECT COUNT(*) AS countRegular FROM Tickets WHERE ticketType = 'Regular'")
            row = cursor.fetchone()
            countRegular = row.countRegular

            cursor.execute("SELECT COUNT(*) AS countVip FROM Tickets WHERE ticketType = 'Vip'")
            row = cursor.fetchone()
            countVip = row.countVip

            return countRegular, countVip
        except pyodbc.Error as e:
            print(e)
            return None, None
    def statsByMovie(self, movieName, sortCriteria):
        try:
            if sortCriteria == 'time':
                cursor.execute("SELECT ticketId, showTime, price FROM Tickets WHERE movieName = ? ORDER BY showTime", (movieName,))
            elif sortCriteria == 'revenue':
                cursor.execute("SELECT ticketId, showTime, price FROM Tickets WHERE movieName = ? ORDER BY price DESC", (movieName,))
            rows = cursor.fetchall()
            for row in rows:
                print(f'Ticket {row.ticketId}: {row.showTime}, {row.price} VND')
        except pyodbc.Error as e:
            print(e)
    def caculateDailyRevenue(self):
        try:
            today = datetime.now().date()
            cursor.execute("SELECT SUM(price) AS totalRevenue FROM Tickets WHERE CONVERT(DATE, showTime) = ?", (today,))
            row = cursor.fetchone()
            totalRevenue = row.totalRevenue if row.totalRevenue else 0
            return totalRevenue
        except pyodbc.Error as e:
            print(e)
            return None
    def displayPendingTickets(self):
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            cursor.execute("SELECT ticketId, showTime FROM Tickets WHERE showTime > ?", current_time)
            rows = cursor.fetchall()
            for row in rows:
                print(f'Pending Ticket {row.ticketId}: {row.showTime}')
        except pyodbc.Error as e:
            print(f'Lỗi khi hiển thị vé đang chờ: {e}')
    def displayRevenueByTimeSlot(self):
        try:
            timeSlots = {"morning": (6, 12), "afternoon": (12, 18), "evening": (18, 24)}
            revenueBySlots = {slot: 0 for slot in timeSlots}
            cursor.execute("SELECT showTime, price FROM Tickets")
            rows = cursor.fetchall()
            for row in rows:
                show_time = datetime.strptime(row.showTime.strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
                for slot, (start, end) in timeSlots.items():
                    if start <= show_time.hour < end:
                        revenueBySlots[slot] += row.price

            for slot, revenue in revenueBySlots.items():
                print(f'Revenue for {slot}: {revenue} VND')
        except pyodbc.Error as e:
            print(e)
    def displayRevenueByMovie(self):
        try:
            revenue_by_movie = {}
            cursor.execute("SELECT movieName, price FROM Tickets")
            rows = cursor.fetchall()
            for row in rows:
                if row.movieName in revenue_by_movie:
                    revenue_by_movie[row.movieName] += row.price
                else:
                    revenue_by_movie[row.movieName] = row.price
            for movie, revenue in revenue_by_movie.items():
                print(f'Revenue for {movie}: {revenue} VND')
        except pyodbc.Error as e:
            print(e)
    def displayTopMovies(self):
        try:
            cursor.execute("SELECT movieName, SUM(price) AS totalRevenue FROM Tickets GROUP BY movieName ORDER BY totalRevenue DESC")
            rows = cursor.fetchmany(5)
            movieRevenue = {}
            for row in rows:
                movieName = row.movieName
                totalRevenue = row.totalRevenue
                if movieName in movieRevenue:
                    movieRevenue[movieName] += totalRevenue
                else:
                    movieRevenue[movieName] = totalRevenue
            for i, (movieName, totalRevenue) in enumerate(movieRevenue.items(), 1):
                print(f'{i}. Movie: {movieName}, Revenue: {totalRevenue} VND')
        except pyodbc.Error as e:
            print(e)
