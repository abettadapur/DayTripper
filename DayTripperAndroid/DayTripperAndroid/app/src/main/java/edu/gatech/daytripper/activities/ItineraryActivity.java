package edu.gatech.daytripper.activities;

import android.app.Fragment;
import android.content.pm.ActivityInfo;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Toast;

import com.facebook.Request;
import com.facebook.Session;
import com.facebook.model.GraphUser;
import com.joanzapata.android.iconify.IconDrawable;
import com.joanzapata.android.iconify.Iconify;
import com.mikepenz.iconics.typeface.FontAwesome;
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

public class ItineraryActivity extends ActionBarActivity implements ItineraryListFragment.ItineraryListListener {

    private ItineraryListFragment itineraryListFragment;
    private SearchItineraryFragment searchItineraryFragment;
    private Fragment currentFragment;
    private RestClient mRestClient;
    private List<Itinerary> itineraries;
    private Drawer.Result mDrawer;
    private AccountHeader.Result mAccountHeader;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intinerary);

        itineraryListFragment = ItineraryListFragment.newInstance();
        searchItineraryFragment = SearchItineraryFragment.newInstance();

        Toolbar toolbar = (Toolbar)findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

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
                                break;
                            case "Search Itineraries":
                                getFragmentManager().beginTransaction().remove(currentFragment).add(R.id.container, searchItineraryFragment).commit();
                                currentFragment = searchItineraryFragment;
                                break;
                            case "Settings":
                                break;
                            case "Logout":
                                break;
                        }


                    }
                })

                .build();

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        overridePendingTransition(R.anim.slide_in, R.anim.slide_out);

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
