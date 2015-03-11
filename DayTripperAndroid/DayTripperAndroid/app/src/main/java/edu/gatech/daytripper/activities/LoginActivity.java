package edu.gatech.daytripper.activities;

import android.content.Intent;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;

import com.facebook.Request;
import com.facebook.Response;
import com.facebook.Session;
import com.facebook.SessionState;
import com.facebook.UiLifecycleHelper;
import com.facebook.model.GraphUser;
import com.facebook.widget.LoginButton;

import java.util.Arrays;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.net.RestClient;
import edu.gatech.daytripper.retro.interfaces.AuthService;
import retrofit.Callback;
import retrofit.RetrofitError;
import edu.gatech.daytripper.net.requests.AuthRequest;


public class LoginActivity extends FragmentActivity {

    private LoginButton authButton;
    private Session.StatusCallback callback = new Session.StatusCallback() {
        @Override
        public void call(Session session, SessionState state, Exception exception)
        {
            onSessionStateChange(session, state, exception);

        }
    };

    private UiLifecycleHelper helper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_login);



        authButton = (LoginButton)findViewById(R.id.authButton);
        authButton.setReadPermissions(Arrays.asList("email", "public_profile"));

        helper = new UiLifecycleHelper(this, callback);
        helper.onCreate(savedInstanceState);
    }

    @Override
    protected void onResume()
    {
        super.onResume();

        Session session = Session.getActiveSession();
        if(session!=null && (session.isOpened() || session.isClosed())){
            onSessionStateChange(session, session.getState(), null);
        }
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

    private void onSessionStateChange(final Session session, SessionState state, Exception exception)
    {
        Log.e("LOGIN", "StateChange");
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

                                Intent i = new Intent(LoginActivity.this, ItineraryActivity.class);
                                i.addCategory(Intent.CATEGORY_HOME);
                                i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                LoginActivity.this.startActivity(i);
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
            //logged out
        }
    }





}
