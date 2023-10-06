from pathlib import Path

ROOT_DIRECTORY = __file__.replace("\\","/").replace(Path(__file__).name,"")#The first replace change windows "\" to "/", second replace remove name of file to get path to directory