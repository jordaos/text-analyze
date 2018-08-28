@echo off
set TOPDIR=%~dp0..
set OPTS=
set MAIN_CLASS=net.sourceforge.pmd.PMD

java -classpath "%TOPDIR%\lib\*;..\lib\pmd-3.4.jar;..\lib\jaxen-1.1-beta-7.jar" %OPTS% %MAIN_CLASS% %*
