# Deploying Your AI Waterborne Disease System to Google Play Store

To get your app on the Play Store, you need to turn this local Python web app into a hosted Android application.

## Step 1: Host the Website (Make it Public)
Google Play Store apps cannot connect to `localhost` or `192.168.x.x`. Your app must be on the public internet.

### Option A: Render (Free Tier)
1.  Push your code to GitHub.
2.  Sign up on [Render.com](https://render.com).
3.  Create a **New Web Service**.
4.  Connect your GitHub repo.
5.  Render will auto-detect Python. Use the following **Start Command**:
    ```bash
    gunicorn app.app:app
    ```

### Option B: PythonAnywhere (Easier Setup)
1.  Sign up on [PythonAnywhere.com](https://www.pythonanywhere.com).
2.  Upload your files.
3.  Configure the WSGI file to point to your Flask app.

## Step 2: Create an Android App Wrapper
Once your site is live (e.g., `https://my-health-app.onrender.com`), you need to wrap it into an Android App Bundle (.aab).

### Option A: Trusted Web Activity (TWA) - Recommended
Google's official way to execute PWAs as native apps.
1.  Use [Bubblewrap CLI](https://github.com/GoogleChromeLabs/bubblewrap).
2.  Run: `bubblewrap init --manifest https://your-site.com/static/manifest.json`
3.  Follow the prompts to generate the Android project.
4.  Run: `bubblewrap build` to get your `.aab` file.

### Option B: Website-to-APK Builders (Easier)
Tools like **AppMySite** or **Median.co** can wrap your URL into an app without coding.

## Step 3: Publish to Google Play Console
1.  Create a Developer Account ($25 one-time fee).
2.  Create a new app listing.
3.  Upload the `.aab` file generated in Step 2.
4.  Fill in store details (Screenshots, Description, Privacy Policy).
5.  Submit for review!

## 🚀 I have prepared the deployment files for you:
-   **Procfile**: For deploying to Render/Heroku.
-   **requirements.txt**: Updated with `gunicorn`.
