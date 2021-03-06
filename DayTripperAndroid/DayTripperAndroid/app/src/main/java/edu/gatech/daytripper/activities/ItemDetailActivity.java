package edu.gatech.daytripper.activities;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.telephony.PhoneNumberUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.RatingBar;
import android.widget.TextView;

import com.facebook.Session;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.MarkerOptions;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.net.RestClient;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class ItemDetailActivity extends ActionBarActivity implements OnMapReadyCallback {

    public static final String ITINERARY_ID_EXTRA = "itinerary_id";
    public static final String ITEM_ID_EXTRA = "item_id";

    private Item currentItem;
    private RestClient mRestClient;

    private TextView mTitleView, mSubtitleView, mReviewCountView;
    private ImageView mImageView;
    private RatingBar mRatingView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_item_detail);

        Toolbar toolbar = (Toolbar)findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        mTitleView = (TextView)findViewById(R.id.titleView);
        //mImageView = (ImageView)findViewById(R.id.imageView);
        mRatingView = (RatingBar)findViewById(R.id.ratingView);
        //mSubtitleView = (TextView)findViewById(R.id.subtitleView);
        mReviewCountView = (TextView)findViewById(R.id.ratingCountView);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        overridePendingTransition(R.anim.slide_in_right, R.anim.slide_out_left);

        mRestClient = new RestClient();
        mRestClient.getItemService().getItem(getIntent().getIntExtra(ITINERARY_ID_EXTRA, 1), getIntent().getIntExtra(ITEM_ID_EXTRA, 1), Session.getActiveSession().getAccessToken(), new Callback<Item>() {
            @Override
            public void success(Item item, Response response) {
                currentItem = item;
                initializeView();
            }

            @Override
            public void failure(RetrofitError error) {

            }
        });

    }

    private void initializeView()
    {
        mTitleView.setText(currentItem.getName());
        //ImageLoader loader = new ImageLoader(mImageView);
        //loader.execute(currentItem.getYelp_entry().getImage_url());
        mRatingView.setRating(currentItem.getYelp_entry().getRating());
        //mSubtitleView.setText(PhoneNumberUtils.formatNumber(currentItem.getYelp_entry().getPhone(), "US"));
        mReviewCountView.setText(" - "+currentItem.getYelp_entry().getReview_count()+" reviews");

        getSupportActionBar().setTitle(currentItem.getCategory());

        MapFragment mapFragment = (MapFragment)getFragmentManager().findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_item_detail, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        switch(id)
        {
            case android.R.id.home:
                finish();
                return true;
            case R.id.action_settings:
                return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onMapReady(GoogleMap googleMap)
    {
        googleMap.addMarker(new MarkerOptions()
                .title(currentItem.getName())
                .snippet(currentItem.getYelp_entry().getLocation().getAddress())
                .position(currentItem.getYelp_entry().getLocation().getCoordinate()));

        googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(currentItem.getYelp_entry().getLocation().getCoordinate(), 13));

    }
}
