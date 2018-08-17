<!-- : Begin batch script
@ECHO OFF
@SETLOCAL ENABLEDELAYEDEXPANSION

IF "x%1" == "x" (
	CALL :ALL
	REM disable echo because subroutine might enable echo
	@ECHO OFF
	IF NOT !ERRORLEVEL! == 0 (
		ECHO ERROR : ALL returned !ERRORLEVEL!
		EXIT /B !ERRORLEVEL!
	)
) else (
	FOR %%i IN (%*) DO (
		CALL :_CHECK_LABEL %%i
		IF !ERRORLEVEL! == 0 (
			CALL :%%i
			REM disable echo because subroutine might enable echo
			@ECHO OFF

			IF NOT !ERRORLEVEL! == 0 (
				ECHO ERROR : %%i returned !ERRORLEVEL!
				EXIT /B !ERRORLEVEL!
			)
		) ELSE (
			ECHO ERROR : no such label, "%%i"
			EXIT /B 1
		)
		
	)
)

@ECHO ON
@EXIT /B !ERRORLEVEL!

REM ===============================
REM === All
REM ===============================
:ALL
CALL :TEXT
@GOTO :EOF

REM ===============================
REM === Text
REM ===============================
:TEXT
ECHO ipy read_text.py  -o text_test.log 日本語のテキスト.txt
ipy read_text.py  -o text_test.log 日本語のテキスト.txt
@GOTO :EOF

REM ===============================
REM === Clean
REM ===============================
:CLEAN
ECHO This is clean.
CSCRIPT //NOLOGO "%~f0?.wsf" //job:Clean
@GOTO :EOF

REM ===============================
REM === _CHECK_LABEL
REM ===============================
:_CHECK_LABEL
FINDSTR /I /R /C:"^[ ]*:%1\>" "%~f0" >NUL 2>NUL
@GOTO :EOF

REM ===============================
REM === END
REM ===============================
:END
@ECHO ON
@EXIT /B !ERRORLEVEL!

----- Begin wsf script --->
<package>
	<job id="Main">
		<?job debug="true"?>
		<script language="JavaScript">
			WScript.Echo("Hello JavaScript World");
			WScript.Quit(1);
		</script>
	</job>

	<job id="Clean">
		<?job debug="true"?>
		<script language="JavaScript">
			WScript.Echo("This is clean job");
			WScript.Quit(1);
		</script>
	</job>
</package>
