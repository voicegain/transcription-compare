How to run TranscribeCompare with python. 

1. First you will need to download python 3. go to https://www.python.org/downloads/ and download the newest verison of python 3. 

2. You will then need to download the transcribe-compare code from github: https://github.com/voicegain/transcription-compare
     Clone the github file to your computer by typing "git clone https://github.com/voicegain/transcription-compare.git" into your git cmd terminal.
	If you want the latest version of the github file later, navigate to where your github file is on your cmd terminal then type "git pull". This will give you the latest update from the repositry. 
	
4. If you do not currenty have "click or inflect" installed on your computer go install them by using these commands "pip install click" and "pip install inflect" 

5. Now to see all the options you have to view your comparison you can type the following "python transcribe-compare --help" this will give you a menu of options depending on how you would like to view your data. 

6. As an example if you would like to view your data in a html file with all lower case and all aligned you would type in the following "python transcribe-compare -R sample_data/The_Princess_and_the_Pea-reference.txt -O sample_data/The_Princess_and_the_Pea-output-1.txt -e WER -a -l -p -j HTML"
    




