FROM python:3.6
WORKDIR /app
ADD . .
EXPOSE 5000
RUN pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt
CMD flask run -h 0.0.0.0 -p 5000
