package edu.gatech.daytripper.activities;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import com.facebook.Session;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.fragments.ItemListFragment;
import edu.gatech.daytripper.fragments.ItineraryListFragment;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ItineraryDetailActivity extends ActionBarActivity implements ItemListFragment.OnFragmentInteractionListener {

    private Itinerary currentItinerary;
    private RestClient mRestClient;
    private ItemListFragment itemListFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_itinerary_detail);

        itemListFragment = ItemListFragment.newInstance();
        if(savedInstanceState==null)
        {
            getFragmentManager().beginTransaction()
                    .add(R.id.container, itemListFragment)
                    .commit();

        }

        int id = getIntent().getIntExtra("itinerary_id", 0);
        mRestClient = new RestClient();

        mRestClient.getItineraryService().getItinerary(id, Session.getActiveSession().getAccessToken(), new Callback<Itinerary>() {
            @Override
            public void success(Itinerary itinerary, Response response) {
                currentItinerary = itinerary;

                //notify fragments
                itemListFragment.updateItems(itinerary.getItems());
                getSupportActionBar().setTitle(itinerary.getName());
            }

            @Override
            public void failure(RetrofitError error) {

            }
        });


    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_itinerary_detail, menu);
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
    public void onFragmentInteraction(String id) {

    }
}
