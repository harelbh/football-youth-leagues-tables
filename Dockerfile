FROM python:3.11-slim

# התקן Chrome ו-ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    git \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# התקן ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+' | head -1) && \
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip -j /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

WORKDIR /app

# התקן Python packages
RUN pip install --no-cache-dir selenium

# העתק את הסקרייפר
COPY render_scraper.py .

# הרץ
CMD ["python", "render_scraper.py"]
