package edu.gatech.daytripper.net;

import com.google.android.gms.maps.model.LatLng;
import com.google.gson.ExclusionStrategy;
import com.google.gson.FieldAttributes;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;
import com.google.gson.annotations.Expose;

import java.lang.reflect.Type;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.GregorianCalendar;

import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.retro.interfaces.AuthService;
import edu.gatech.daytripper.retro.interfaces.CategoryService;
import edu.gatech.daytripper.retro.interfaces.DirectionsService;
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
    private DirectionsService directionsService;
    private CategoryService categoryService;

    public RestClient()
    {
        Gson gson = new GsonBuilder()
                .registerTypeAdapter(Calendar.class, new CalendarSerializer())
                .registerTypeAdapter(GregorianCalendar.class, new CalendarSerializer())
                .registerTypeAdapter(LatLng.class, new LatLngSerializer())
                .setDateFormat("yyyy-MM-dd'T'HH:mmZ")
                .addSerializationExclusionStrategy(new ExclusionStrategy() {
                    @Override
                    public boolean shouldSkipField(FieldAttributes fieldAttributes) {
                        final Expose expose = fieldAttributes.getAnnotation(Expose.class);
                        return expose != null && !expose.serialize();
                    }

                    @Override
                    public boolean shouldSkipClass(Class<?> aClass) {
                        return false;
                    }
                })
                .addDeserializationExclusionStrategy(new ExclusionStrategy() {
                    @Override
                    public boolean shouldSkipField(FieldAttributes fieldAttributes) {
                        final Expose expose = fieldAttributes.getAnnotation(Expose.class);
                        return expose != null && !expose.deserialize();
                    }

                    @Override
                    public boolean shouldSkipClass(Class<?> aClass) {
                        return false;
                    }
                })
                .create();

        RestAdapter adapter = new RestAdapter.Builder()
                .setLogLevel(RestAdapter.LogLevel.BASIC)
                .setEndpoint(BASE_URL)
                .setConverter(new GsonConverter(gson))
                .build();


        authService = adapter.create(AuthService.class);
        itineraryService = adapter.create(ItineraryService.class);
        itemService = adapter.create(ItemService.class);
        directionsService = adapter.create(DirectionsService.class);
        categoryService = adapter.create(CategoryService.class);

    }

    public AuthService getAuthService()
    {
        return authService;
    }
    public ItineraryService getItineraryService() { return itineraryService; }
    public ItemService getItemService() { return itemService; }
    public DirectionsService getDirectionsService() { return directionsService; }
    public CategoryService getCategoryService(){ return categoryService; }

    private class CalendarSerializer implements JsonSerializer<Calendar>, JsonDeserializer<Calendar>
    {

        @Override
        public Calendar deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
            String date_str = json.getAsString();
            Calendar date = null;
            try {
                sdf.parse(date_str);
                date = sdf.getCalendar();
            }
            catch(ParseException pex)
            {
                throw new IllegalStateException("Parse Error: "+date_str);
            }
            return date;
        }

        @Override
        public JsonElement serialize(Calendar src, Type typeOfSrc, JsonSerializationContext context) {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
            return new JsonPrimitive(sdf.format(src.getTime()));
        }
    }

    private class LatLngSerializer implements JsonSerializer<LatLng>, JsonDeserializer<LatLng>
    {
        @Override
        public LatLng deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
            JsonObject coordinate = (JsonObject)json;

            return new LatLng(coordinate.getAsJsonPrimitive("latitude").getAsDouble(), coordinate.getAsJsonPrimitive("longitude").getAsDouble());
        }

        @Override
        public JsonElement serialize(LatLng src, Type typeOfSrc, JsonSerializationContext context) {
            return new JsonPrimitive(src.latitude+", "+src.longitude);
        }
    }


}
