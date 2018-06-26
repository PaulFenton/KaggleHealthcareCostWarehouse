IF OBJECT_ID('dbo.Fact', 'U') IS NOT NULL
  DROP TABLE dbo.Fact;
IF OBJECT_ID('dbo.dim_Time', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Time;
IF OBJECT_ID('dbo.dim_Facility', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Facility;
IF OBJECT_ID('dbo.dim_Classifications_Diag', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Classifications_Diag;
IF OBJECT_ID('dbo.dim_Classifications_Proc', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Classifications_Proc;
IF OBJECT_ID('dbo.dim_Patients_Refine', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Patients_Refine;
IF OBJECT_ID('dbo.dim_Patient', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Patient;
IF OBJECT_ID('dbo.dim_Payment', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Payment;
IF OBJECT_ID('dbo.dim_Provider', 'U') IS NOT NULL
  DROP TABLE dbo.dim_Provider;

CREATE TABLE dim_Facility(
	Facility_Key int NOT NULL IDENTITY(1,1),
	[Facility ID] int NOT NULL,
	[Health Service Area] varchar(50),
	[Hospital County] varchar(50),
	[Operating Certificate Number] integer,
	[Facility Name] varchar(255),
	[Active Flag] smallint NOT NULL DEFAULT 1,
	[Effective Start Date] datetime,
	[Effective End Date] datetime
)

CREATE TABLE dim_Patient(
	Patient_Key int NOT NULL IDENTITY(1,1),
	[Age Group] nvarchar(50),
	[ip Code - 3 digits] int,
	Gender varchar(5),
	Race varchar(50),
	Ethnicity varchar(50),
	[Patient Disposition] varchar(255)
)

CREATE TABLE dim_Time(
	Time_Key int NOT NULL IDENTITY(1,1),
	[Discharge Date] datetime
)

CREATE TABLE dim_Classifications_Diag(
	Classifications_Diag_Key int NOT NULL IDENTITY(1,1),
	[CCS Diagnosis Code] int,
	[CCS Diagnosis Description] varchar(255)
)

CREATE TABLE dim_Classifications_Proc(
	Classifications_Proc_Key int NOT NULL IDENTITY(1,1),
	[CCS Procedure Code] varchar(10),
	[CCS Procedure Description] varchar(255)
)
CREATE TABLE dim_Patients_Refine(
	Patients_Refine_Key int NOT NULL IDENTITY(1,1),
	[ID Patients Refine] int,
	[APR DRG Code] int,
	[APR Risk of Mortality] varchar(50)
)

CREATE TABLE dim_Payment(
	Payment_Key int NOT NULL IDENTITY(1,1),
	[Payment ID] int,
	[Payment Typology 1] varchar(255),
	[Payment Typology 2] varchar(255),
	[Payment Typology 3] varchar(255)
)

CREATE TABLE dim_Provider(
	Provider_Key int NOT NULL IDENTITY(1,1),
	[Provider License Number] int,
)

alter table dim_Facility add primary key (Facility_Key);
alter table dim_Patient add primary key (Patient_Key);
alter table dim_Time add primary key (Time_Key);
alter table dim_Classifications_Diag add primary key (Classifications_Diag_key);
alter table dim_Classifications_Proc add primary key (Classifications_Proc_Key);
alter table dim_Patients_Refine add primary key (Patients_Refine_Key);
alter table dim_Payment add primary key (Payment_Key);
alter table dim_Provider add primary key (Provider_Key);

CREATE TABLE Fact(

	Time_Key int NOT NULL,
	Facility_Key int NOT NULL,
	Classifications_Diag_Key int NOT NULL,
	Classifications_Proc_Key int NOT NULL,
	Patients_Refine_Key int NOT NULL,
	Patient_Key int NOT NULL,
	Payment_Key int NOT NULL,
	Provider_Key int NOT NULL,
	[Total Costs] numeric(10, 2) NULL,
	[Total Charges] numeric(10, 2) NULL,
	[Ratio of Total Costs to Total Charges] numeric(5, 2) NULL

);

alter table Fact add constraint FK_Time
foreign key (Time_Key) references dim_Time (Time_Key);

alter table Fact add constraint FK_Facility
foreign key (Facility_Key) references dim_Facility (Facility_Key);

alter table Fact add constraint FK_Classifications_Diag
foreign key (Classifications_Diag_Key) references dim_Classifications_Diag (Classifications_Diag_Key);

alter table Fact add constraint FK_Classifications_Proc
foreign key (Classifications_Proc_Key) references dim_Classifications_Proc (Classifications_Proc_Key);

alter table Fact add constraint FK_Patients_Refine
foreign key (Patients_Refine_Key) references dim_Patients_Refine (Patients_Refine_Key);

alter table Fact add constraint FK_Patient
foreign key (Patient_Key) references dim_Patient (Patient_Key);

alter table Fact add constraint FK_Payment
foreign key (Payment_Key) references dim_Payment (Payment_Key);

alter table Fact add constraint FK_Provider
foreign key (Provider_Key) references dim_Provider (Provider_Key)