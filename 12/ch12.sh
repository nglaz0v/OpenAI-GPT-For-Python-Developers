
sudo npm install -g @vue/cli

mkdir chatbot chatbot/server
cd chatbot
vue create client

cd client
vue add router
cd ..

sudo npm install axios --save

pip3 install Flask Flask-Cors

cd server
python3 app.py
cd ..

cd client
npm run serve
cd ..
