package edu.gatech.daytripper.activities;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import com.facebook.Request;
import com.facebook.Response;
import com.facebook.Session;
import com.facebook.model.GraphUser;

import java.util.Timer;
import java.util.TimerTask;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import edu.gatech.daytripper.net.requests.AuthRequest;
import edu.gatech.daytripper.retro.interfaces.AuthService;
import retrofit.Callback;
import retrofit.RetrofitError;

public class SplashActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                checkLogin();
            }
        }, 0, 10000);
    }

    private void checkLogin()
    {
        final Session session = Session.getActiveSession();
        if(session!=null && session.isOpened())
        {
//            Request request = Request.newMeRequest(session, new Request.GraphUserCallback() {
//                @Override
//                public void onCompleted(GraphUser user, Response response) {
//                    if (user != null) {
//                        final String user_ID = user.getId();
//                        final String token = session.getAccessToken();
//
//                        //check this authentication
//                        AuthService auth = new RestClient().getAuthService();
//                        auth.verifyAuthentication(new AuthRequest(token, user_ID), new Callback<Boolean>() {
//                            @Override
//                            public void success(Boolean aBoolean, retrofit.client.Response response) {
//                                Log.e("LOGIN", "Login was successful, launch new activity");
//                                Log.e("Token", token);
//                                Log.e("User", user_ID);
//
//                                Intent i = new Intent(SplashActivity.this, ItineraryActivity.class);
//                                startActivity(i);
//
//
//                            }
//
//                            @Override
//                            public void failure(RetrofitError error) {
//                                Log.e("LOGIN", error.getMessage());
//                                Log.e("LOGIN", "Login failed, verification was ");
//                                Log.e("Token", token);
//                                Log.e("User", user_ID);
//
//                                Intent i = new Intent(SplashActivity.this, LoginActivity.class);
//                                startActivity(i);
//                            }
//                        });
//                    }
//                }
//            });
//            request.executeAsync();
            Intent i = new Intent(this, ItineraryActivity.class);
            startActivity(i);
        }
        else
        {
            Intent i = new Intent(this, LoginActivity.class);
            startActivity(i);
        }
        finish();
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
}
