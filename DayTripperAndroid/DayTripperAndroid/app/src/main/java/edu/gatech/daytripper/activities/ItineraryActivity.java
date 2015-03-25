package edu.gatech.daytripper.activities;

import android.content.pm.ActivityInfo;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import com.facebook.Session;

import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.fragments.ItineraryListFragment;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ItineraryActivity extends ActionBarActivity implements ItineraryListFragment.ItineraryListListener {

    private ItineraryListFragment itineraryListFragment;
    private RestClient mRestClient;
    private List<Itinerary> itineraries;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intinerary);

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        overridePendingTransition(R.anim.slide_in, R.anim.slide_out);

        /**Create a new itinerary list fragment and add it to the activity **/
        itineraryListFragment = ItineraryListFragment.newInstance();
        if(savedInstanceState==null)
        {
            getFragmentManager().beginTransaction()
                    .add(R.id.container, itineraryListFragment)
                    .commit();

        }
        mRestClient = new RestClient();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_intinerary, menu);
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

    @Override
    public void refresh_list(final ItineraryListFragment fragment)
    {
        /** Get a listing of the itineraries for the current user and update the fragment with the items **/
        mRestClient.getItineraryService().listItineraries(Session.getActiveSession().getAccessToken(), new Callback<List<Itinerary>>() {
            @Override
            public void success(List<Itinerary> itineraries, Response response) {
                ItineraryActivity.this.itineraries = itineraries;
                fragment.updateItems(itineraries);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.e("GET ITINERARIES", error.getMessage());
            }
        });

    }
}
