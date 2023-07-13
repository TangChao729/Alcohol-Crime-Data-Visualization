# pull official base image
FROM node:20-alpine3.16

# set base usl and port
# docker run -e REACT_APP_BASE_URL=http://example.com:5000/ your-image-name
ENV REACT_APP_BASE_URL=http://localhost:5000/

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent
RUN npm install --save react react-dom react-scripts --silent

# add app
COPY . .
# RUN npm build
#EXPOSE 3000

# start app
CMD ["npm", "start"]

