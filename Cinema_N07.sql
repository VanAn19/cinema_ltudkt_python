create database Cinema_N07
go

use Cinema_N07
go

create table Tickets(
	ticketId int primary key,
	room nvarchar(50) not null, 
	movieName nvarchar(50) not null,
	showTime datetime not null,
	seatPosition nvarchar(10) not null,
	ticketType nvarchar(10) not null,
	price int not null
)

select * from Tickets

INSERT INTO [dbo].[Tickets]
           ([ticketId]
		   ,[room]
		   ,[movieName]
		   ,[showTime]
		   ,[seatPosition]
		   ,[ticketType]
           ,[price])
     VALUES
           ('211'
           ,N'1'
		   ,N'Iron Man'
		   ,'2024/02/19 14:00'
		   ,N'H8'
		   ,N'Vip'
		   ,'100000')
GO