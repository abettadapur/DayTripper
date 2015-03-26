package edu.gatech.daytripper.activities;

import android.content.pm.ActivityInfo;
import android.location.Address;
import android.location.Geocoder;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import com.facebook.Session;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.melnykov.fab.FloatingActionButton;

import java.io.IOException;
import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.fragments.ItemListFragment;
import edu.gatech.daytripper.fragments.ItineraryListFragment;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ItineraryDetailActivity extends ActionBarActivity implements ItemListFragment.ItemListListener, OnMapReadyCallback, View.OnClickListener {

    private Itinerary currentItinerary;
    private RestClient mRestClient;
    private ItemListFragment itemListFragment;
    private FloatingActionButton mFab;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_itinerary_detail);

        Toolbar toolbar = (Toolbar)findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        overridePendingTransition(R.anim.slide_in, R.anim.slide_out_right);
        itemListFragment = ItemListFragment.newInstance();
        if(savedInstanceState==null)
        {
            getFragmentManager().beginTransaction()
                    .add(R.id.container, itemListFragment)
                    .commit();

        }

        int id = getIntent().getIntExtra("itinerary_id", 0);

        mFab = (FloatingActionButton)findViewById(R.id.edit_fab);
        mFab.setOnClickListener(this);
        mRestClient = new RestClient();

        mRestClient.getItineraryService().getItinerary(id, Session.getActiveSession().getAccessToken(), new Callback<Itinerary>() {
            @Override
            public void success(Itinerary itinerary, Response response) {
                currentItinerary = itinerary;

                //notify fragments
                itemListFragment.updateItems(itinerary.getItems());
                getSupportActionBar().setTitle(itinerary.getName());

                MapFragment mapFragment = (MapFragment)getFragmentManager().findFragmentById(R.id.map);
                mapFragment.getMapAsync(ItineraryDetailActivity.this);

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
        switch (item.getItemId())
        {
            case android.R.id.home:
                finish();
                overridePendingTransition(R.anim.slide_out, R.anim.slide_in);
                return true;
            case R.id.action_settings:
                return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public void refresh_list(final ItemListFragment fragment)
    {

    }

    @Override
    public Itinerary getItinerary() {
        return currentItinerary;
    }

    @Override
    public void onMapReady(GoogleMap googleMap)
    {
        Geocoder coder = new Geocoder(this);
        try {
            List<Address> addresses = coder.getFromLocationName(currentItinerary.getCity(), 1);
            LatLng city =  new LatLng(addresses.get(0).getLatitude(), addresses.get(0).getLongitude());
            googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(city, 10));
        }
        catch(IOException ioex)
        {}

        for(Item i: currentItinerary.getItems())
        {
            googleMap.addMarker(new MarkerOptions()
                    .title(i.getName())
                    .snippet(i.getYelp_entry().getLocation().getAddress())
                    .position(i.getYelp_entry().getLocation().getCoordinate()));
        }

    }

    @Override
    public void onClick(View v) {

    }
}
