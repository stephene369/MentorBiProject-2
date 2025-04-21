@echo off

REM Script to add, commit and push Git changes

git add .

REM Get current date and time in format DD/MM/YYYY/HH-MM-SS
@echo off
for /f %%A in ('powershell -command "Get-Date -Format \"dd/MM/yyyy/HH-mm-ss\" "') do set current_date=%%A

echo %current_date%

git commit -m "Version-%current_date%"
git push
echo Commit and push completed successfully!
