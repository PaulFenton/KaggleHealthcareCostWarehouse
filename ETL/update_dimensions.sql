update dim_Classifications_Diag
set [active flag] = 0
where [CCS Diagnosis Code] in (1,2,219);

update dim_Classifications_Diag
set [Effective End Date] = '10/1/2017'
where [CCS Diagnosis Code] in (1,2,219);

update dim_Classifications_Proc
set [active flag] = 0
where [CCS Procedure Code] in (37,110,169);

update dim_Classifications_Proc
set [Effective End Date] = '10/1/2017'
where [CCS Procedure Code] in (37,110,169);

update dim_Facility
set [active flag] = 0
where [Facility Id] in (165,170,174);

update dim_Facility
set [Effective End Date] = '10/1/2017'
where [Facility Id] in (165,170,174)