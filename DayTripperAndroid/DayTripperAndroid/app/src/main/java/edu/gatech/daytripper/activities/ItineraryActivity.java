package edu.gatech.daytripper.activities;

import android.app.Fragment;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.widget.SearchView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;

import com.facebook.Request;
import com.facebook.Session;
import com.facebook.model.GraphUser;
import com.joanzapata.android.iconify.IconDrawable;
import com.joanzapata.android.iconify.Iconify;
import com.mikepenz.materialdrawer.Drawer;
import com.mikepenz.materialdrawer.accountswitcher.AccountHeader;
import com.mikepenz.materialdrawer.model.PrimaryDrawerItem;
import com.mikepenz.materialdrawer.model.ProfileDrawerItem;
import com.mikepenz.materialdrawer.model.SecondaryDrawerItem;
import com.mikepenz.materialdrawer.model.SectionDrawerItem;
import com.mikepenz.materialdrawer.model.interfaces.IDrawerItem;
import com.mikepenz.materialdrawer.model.interfaces.Nameable;

import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.fragments.ItineraryListFragment;
import edu.gatech.daytripper.fragments.SearchItineraryFragment;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ItineraryActivity extends ActionBarActivity implements ItineraryListFragment.ItineraryListListener, SearchView.OnQueryTextListener {

    private ItineraryListFragment itineraryListFragment;
    private ItineraryListFragment searchItineraryFragment;
    private Fragment currentFragment;
    private RestClient mRestClient;
    private List<Itinerary> itineraries;
    private Drawer.Result mDrawer;
    private AccountHeader.Result mAccountHeader;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intinerary);

        itineraryListFragment = ItineraryListFragment.newInstance(R.layout.fragment_itinerary_list, R.layout.itinerary_list_item);
        searchItineraryFragment = ItineraryListFragment.newInstance(R.layout.fragment_search_itinerary, R.layout.itinerary_list_item);

        Toolbar toolbar = (Toolbar)findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        toolbar.setNavigationIcon(new IconDrawable(this, Iconify.IconValue.fa_reorder).color(0xFFFFFF).sizeDp(23));
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDrawer.openDrawer();
            }
        });

        mAccountHeader = new AccountHeader()
                .withActivity(this)
                .withHeaderBackground(R.drawable.header)
                .build();

        Request request = Request.newMeRequest(Session.getActiveSession(), new Request.GraphUserCallback() {
            @Override
            public void onCompleted(GraphUser graphUser, com.facebook.Response response) {
                mAccountHeader.addProfile(new ProfileDrawerItem().withName(graphUser.getName()), 0);
            }
        });
        request.executeAsync();

        mDrawer = new Drawer()
                .withActivity(this)
                .withTranslucentStatusBar(false)
                .withActionBarDrawerToggle(true)
                .withAccountHeader(mAccountHeader)
                .addDrawerItems(
                        new PrimaryDrawerItem().withName("My Itineraries").withIcon(new IconDrawable(this, Iconify.IconValue.fa_list).color(0xFFFFFF)),
                        new PrimaryDrawerItem().withName("Search Itineraries").withIcon(new IconDrawable(this, Iconify.IconValue.fa_search).color(0xFFFFFF)),

                        new SectionDrawerItem(),
                        new SecondaryDrawerItem().withName("Settings").withIcon(new IconDrawable(this, Iconify.IconValue.fa_cog).color(0xFFFFFF)),
                        new SecondaryDrawerItem().withName("Logout").withIcon(new IconDrawable(this, Iconify.IconValue.fa_sign_out).color(0xFFFFFF))
                )
                .withOnDrawerItemClickListener(new Drawer.OnDrawerItemClickListener() {

                    @Override
                    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l, IDrawerItem iDrawerItem) {
                        String item = ((Nameable) iDrawerItem).getName();
                        switch (item) {
                            case "My Itineraries":
                                getFragmentManager().beginTransaction().remove(currentFragment).add(R.id.container, itineraryListFragment).commit();
                                currentFragment = itineraryListFragment;
                                getSupportActionBar().setTitle("Your Itineraries");
                                break;
                            case "Search Itineraries":
                                getFragmentManager().beginTransaction().remove(currentFragment).add(R.id.container, searchItineraryFragment).commit();
                                currentFragment = searchItineraryFragment;
                                getSupportActionBar().setTitle("Search Results");
                                break;
                            case "Settings":
                                break;
                            case "Logout":
                                Session.getActiveSession().closeAndClearTokenInformation();
                                Intent intent = new Intent(ItineraryActivity.this, SplashActivity.class);
                                intent.putExtra("delay", false);
                                startActivity(intent);
                                finish();
                                break;
                        }


                    }
                })

                .build();

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        overridePendingTransition(R.anim.slide_in_right, R.anim.slide_out_left);

        /**Create a new itinerary list fragment and add it to the activity **/


        if(savedInstanceState==null)
        {
            getFragmentManager().beginTransaction()
                    .add(R.id.container, itineraryListFragment)
                    .commit();
            currentFragment = itineraryListFragment;

        }
        mRestClient = new RestClient();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_intinerary, menu);

        SearchView view = (SearchView)menu.findItem(R.id.search).getActionView();
        if(view!=null)
        {
            view.setOnQueryTextListener(this);
        }

        return super.onCreateOptionsMenu(menu);
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
        if(fragment==itineraryListFragment) {
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

    @Override
    public boolean onQueryTextSubmit(String s) {
        if(!s.equals("")) {
            if (currentFragment == itineraryListFragment) {
                mDrawer.setSelection(1);
            }
            mRestClient.getItineraryService().searchItinerary(s, Session.getActiveSession().getAccessToken(), new Callback<List<Itinerary>>() {
                @Override
                public void success(List<Itinerary> itineraries, Response response) {
                    searchItineraryFragment.updateItems(itineraries);
                }

                @Override
                public void failure(RetrofitError error) {

                }
            });
        }


        return true;
    }

    @Override
    public boolean onQueryTextChange(String s) {
        return false;
    }
}
