package edu.gatech.daytripper.activities;

import android.app.Activity;
import android.content.Intent;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ProgressBar;

import com.facebook.Request;
import com.facebook.Response;
import com.facebook.Session;
import com.facebook.SessionState;
import com.facebook.UiLifecycleHelper;
import com.facebook.model.GraphUser;
import com.facebook.widget.LoginButton;

import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import edu.gatech.daytripper.net.requests.AuthRequest;
import edu.gatech.daytripper.retro.interfaces.AuthService;
import retrofit.Callback;
import retrofit.RetrofitError;

public class SplashActivity extends FragmentActivity {

    private LoginButton authButton;
    private ProgressBar progressBar;
    private Session.StatusCallback callback = new Session.StatusCallback() {
        @Override
        public void call(Session session, SessionState state, Exception exception)
        {
            onSessionStateChange(session, state, exception);

        }
    };

    private UiLifecycleHelper helper;
    private boolean started;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        authButton = (LoginButton)findViewById(R.id.authButton);
        authButton.setReadPermissions(Arrays.asList("email", "public_profile"));
        progressBar = (ProgressBar)findViewById(R.id.progressBar);
        helper = new UiLifecycleHelper(this, callback);
        helper.onCreate(savedInstanceState);
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        Bundle extras = getIntent().getExtras();
        if(extras==null || extras.getBoolean("delay", true)) {
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    checkLogin();
                }
            }, 5000);
        }
        else
            checkLogin();

        helper.onResume();

    }
    @Override
    protected void onPause()
    {
        super.onPause();
        helper.onPause();
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        helper.onDestroy();
    }


    @Override
    public void onSaveInstanceState(Bundle outState)
    {
        super.onSaveInstanceState(outState);
        helper.onSaveInstanceState(outState);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        super.onActivityResult(requestCode, resultCode, data);
        helper.onActivityResult(requestCode, resultCode, data);
    }

    private void checkLogin()
    {
        Session session = Session.getActiveSession();
        if(session!=null && (session.isOpened() || session.isClosed())){
            onSessionStateChange(session, session.getState(), null);
        }
        else
        {
            authButton.setVisibility(View.VISIBLE);
            progressBar.setVisibility(View.INVISIBLE);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_splash, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private void onSessionStateChange(final Session session, SessionState state, Exception exception)
    {
        if(state.isOpened()){
            //authenticated
            Log.e("LOGIN", "Authenticated");
            Request request = Request.newMeRequest(session, new Request.GraphUserCallback() {
                @Override
                public void onCompleted(GraphUser user, Response response)
                {
                    if(user!=null)
                    {
                        final String user_ID = user.getId();
                        final String token = session.getAccessToken();

                        //check this authentication
                        AuthService auth = new RestClient().getAuthService();
                        auth.verifyAuthentication(new AuthRequest(token, user_ID), new Callback<Boolean>() {
                            @Override
                            public void success(Boolean aBoolean, retrofit.client.Response response) {
                                Log.e("LOGIN", "Login was successful, launch new activity");
                                Log.e("Token", token);
                                Log.e("User", user_ID);

                                if(!started) {
                                    Intent i = new Intent(SplashActivity.this, ItineraryActivity.class);
                                    i.addCategory(Intent.CATEGORY_HOME);
                                    i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                    SplashActivity.this.startActivity(i);
                                    started = true;
                                    finish();
                                }
                            }

                            @Override
                            public void failure(RetrofitError error) {
                                Log.e("LOGIN", error.getMessage());
                                Log.e("LOGIN", "Login failed, verification was ");
                                Log.e("Token", token);
                                Log.e("User", user_ID);
                            }
                        });

                        //on success, forward to next activity

                    }
                }

            });
            request.executeAsync();

        }
        else if(state.isClosed())
        {
            authButton.setVisibility(View.VISIBLE);
            progressBar.setVisibility(View.INVISIBLE);
        }
    }
}
