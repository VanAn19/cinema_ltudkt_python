from Ticket import Ticket
from ManageTicket import ManageTicket

def main():
    ticketManager = ManageTicket()
    while True:
        print("-------------------------------------------------------------")
        print("1. Bán vé mới") 
        print("2. Hủy vé đã bán") 
        print("3. Thống kê số lượng vé đã bán của mỗi loại vé") 
        print("4. Thống kê thông tin vé đã bán theo tên phim (time/revenue)") 
        print("5. Tính tổng doanh thu từ vé đã bán của ngày hiện tại") 
        print("6. Hiển thị danh sách các vé đang chờ xem theo thời gian") 
        print("7. Hiển thị doanh thu theo khung thời gian chiếu phim") 
        print("8. Hiển thị doanh thu theo phim") 
        print("9. Hiển thị top 5 phim có doanh thu cao nhất") 
        print("0. Thoát chương trình") 
        print("-------------------------------------------------------------")
        
        choice = input("Chọn chức năng: ")
        
        if choice == '1':
            ticketId = input("Nhập mã vé: ")
            room = input("Nhập phòng chiếu: ")
            movieName = input("Nhập tên phim: ")
            showTime = input("Nhập thời gian chiếu (YYYY-MM-DD HH:MM): ")
            seatPosition = input("Nhập vị trí ghế: ")
            ticketType = input("Nhập loại vé (Regular/Vip): ")
            price = int(input("Nhập giá vé: "))
            newTicket = Ticket(ticketId, room, movieName, showTime, seatPosition, ticketType, price)
            ticketManager.sellTicket(newTicket)
            # print(f'Đã bán vé {newTicket.ticketId}')
            
        elif choice == '2':
            ticketIdCancel = input("Nhập mã vé cần hủy: ")
            ticketManager.cancelTicket(ticketIdCancel)
            print(f'Đã hủy vé {ticketIdCancel} thành công!')
            
        elif choice == '3':
            countRegular, countVip = ticketManager.countTicketsByType()
            print(f"Số lượng vé Regular đã bán: {countRegular}")
            print(f"Số lượng vé Vip đã bán: {countVip}")
            
        elif choice == '4':
            movieNameToStats = input("Nhập tên phim cần thống kê: ")
            sortCriteria = input("Nhập tiêu chí sắp xếp (time/revenue): ")
            ticketManager.statsByMovie(movieNameToStats, sortCriteria)
            
        elif choice == '5':
            totalRevenue = ticketManager.caculateDailyRevenue()
            print(f'Tổng doanh thu từ vé đã bán hôm nay: {totalRevenue} VND')
        
        elif choice == '6':
            ticketManager.displayPendingTickets()
        
        elif choice == '7':
            ticketManager.displayRevenueByTimeSlot()
            
        elif choice == '8':
            ticketManager.displayRevenueByMovie()
            
        elif choice == '9':
            ticketManager.displayTopMovies()
            
        elif choice == '0':
            print("Chương trình kết thúc")
            break
        
        else:
            print("Lựa chọn không hợp lệ. Hãy chọn lại")
            
if (__name__ == "__main__"):
    main()