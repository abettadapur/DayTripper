package edu.gatech.daytripper.retro.interfaces;

import java.util.Dictionary;

import edu.gatech.daytripper.net.requests.AuthRequest;
import retrofit.Callback;
import retrofit.http.Body;
import retrofit.http.POST;

/**
 * Created by Alex on 2/19/2015.
 */
public interface AuthService {
    @POST("/auth/verify")
    void verifyAuthentication(@Body AuthRequest postBody, Callback<Boolean> callback);

}
