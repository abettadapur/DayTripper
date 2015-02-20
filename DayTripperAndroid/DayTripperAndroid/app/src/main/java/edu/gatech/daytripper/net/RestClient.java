package edu.gatech.daytripper.net;

import edu.gatech.daytripper.retro.interfaces.AuthService;
import retrofit.RestAdapter;

/**
 * Created by Alex on 2/19/2015.
 */
public class RestClient {

    private static final String BASE_URL="http://192.168.1.7:5000";
    private AuthService authService;

    public RestClient()
    {
        RestAdapter adapter = new RestAdapter.Builder()
                .setLogLevel(RestAdapter.LogLevel.FULL)
                .setEndpoint(BASE_URL)
                .build();

        authService = adapter.create(AuthService.class);
    }

    public AuthService getAuthService()
    {
        return authService;
    }

}
