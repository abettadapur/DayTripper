package edu.gatech.daytripper.retro.interfaces;

import java.util.List;

import edu.gatech.daytripper.model.YelpEntry;
import retrofit.Callback;
import retrofit.http.GET;
import retrofit.http.Path;
import retrofit.http.Query;

/**
 * Created by Alex on 3/7/2015.
 */
public interface CategoryService
{
    @GET("/category/{category}/query")
    public void searchCategory(@Path("category") String category, @Query("location") String city, @Query("token") String token, Callback<List<YelpEntry>> callback);
}
