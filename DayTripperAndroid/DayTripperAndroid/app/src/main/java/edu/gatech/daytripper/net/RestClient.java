package edu.gatech.daytripper.net;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.text.DateFormat;

import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.retro.interfaces.AuthService;
import edu.gatech.daytripper.retro.interfaces.ItemService;
import edu.gatech.daytripper.retro.interfaces.ItineraryService;
import retrofit.RestAdapter;
import retrofit.converter.GsonConverter;

/**
 * Created by Alex on 2/19/2015.
 */
public class RestClient {

    private static final String BASE_URL="http://bettadapur.com:3000";
    private AuthService authService;
    private ItineraryService itineraryService;
    private ItemService itemService;

    public RestClient()
    {
        Gson gson = new GsonBuilder()
                .setDateFormat("yyyy-MM-dd'T'HH:mmZ")
                .create();

        RestAdapter adapter = new RestAdapter.Builder()
                .setLogLevel(RestAdapter.LogLevel.FULL)
                .setEndpoint(BASE_URL)
                .setConverter(new GsonConverter(gson))
                .build();


        authService = adapter.create(AuthService.class);
        itineraryService = adapter.create(ItineraryService.class);
        itemService = adapter.create(ItemService.class);
    }

    public AuthService getAuthService()
    {
        return authService;
    }
    public ItineraryService getItineraryService() { return itineraryService; }
    public ItemService getItemService() { return itemService; }

}
