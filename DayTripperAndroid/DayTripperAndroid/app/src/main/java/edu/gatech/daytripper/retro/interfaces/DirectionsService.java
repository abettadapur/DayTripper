package edu.gatech.daytripper.retro.interfaces;

import com.google.android.gms.maps.model.LatLng;

import edu.gatech.daytripper.model.Directions;
import retrofit.Callback;
import retrofit.http.GET;
import retrofit.http.Query;

/**
 * Created by Alex on 3/30/2015.
 */
public interface DirectionsService
{
    @GET("/maps/directions")
    public void getDirections(@Query("origin")String origin, @Query("destination") String destination , @Query("token") String token, Callback<Directions> callback);

    @GET("/maps/polyline")
    public void getPolyline(@Query("origin")String origin, @Query("destination") String destination , @Query("token") String token, Callback<String> callback);
}
