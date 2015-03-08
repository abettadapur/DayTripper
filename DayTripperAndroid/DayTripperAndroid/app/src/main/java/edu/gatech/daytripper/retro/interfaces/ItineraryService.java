package edu.gatech.daytripper.retro.interfaces;

import edu.gatech.daytripper.model.Itinerary;
import retrofit.Callback;
import retrofit.http.Body;
import retrofit.http.DELETE;
import retrofit.http.GET;
import retrofit.http.POST;
import retrofit.http.PUT;
import retrofit.http.Path;
import retrofit.http.Query;

/**
 * Created by Alex on 3/7/2015.
 */
public interface ItineraryService
{
    @POST("/itinerary/create")
    public void createItinerary(@Body Itinerary itinerary, @Query("token") String token, Callback<Itinerary> callback);

    @GET("/itinerary/{id}")
    public void getItinerary(@Path("id") int id, @Query("token") String token, Callback<Itinerary> callback);

    @PUT("/itinerary/{id}")
    public void updateItinerary(@Path("id") int id, @Body Itinerary itinerary, @Query("token") String token, Callback<Itinerary> callback);

    @DELETE("/itinerary/{id}")
    public void deleteItinerary(@Path("id") int id, @Query("token") String token, Callback<Boolean> callback);
}
