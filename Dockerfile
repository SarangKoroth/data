FROM python:3.6

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update --fix-missing
RUN apt-get install -y google-chrome-stable
RUN google-chrome-stable --version
RUN which google-chrome-stable
# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN which chromedriver
RUN /usr/local/bin/chromedriver --version

# set display port to avoid crash
ENV DISPLAY=:99

# Install requirements first so this step is cached by Docker
COPY requirements.txt c:/Users/Admin/Desktop/my_version_yelp/yelpscraper/requirements.txt
WORKDIR c:/Users/Admin/Desktop/my_version_yelp/yelpscraper
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy code
COPY database_code.py database_code.py
COPY yelpscraper_ec2.py yelpscraper_ec2.py
#RUN python yelpscraper_ec2.py
ENTRYPOINT ["python","yelpscraper_ec2.py"]

