package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.telephony.PhoneNumberUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RatingBar;
import android.widget.TextView;



import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Item;

/**
 * Created by Alex on 3/30/2015.
 */
public class ItemDetailFragment extends Fragment
{

    private Item currentItem;
    private TextView mTitleView, mSubtitleView, mReviewCountView;
    private RatingBar mRatingView;


    public static ItemDetailFragment newInstance()
    {
        ItemDetailFragment fragment = new ItemDetailFragment();
        return fragment;
    }
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        View v = inflater.inflate(R.layout.fragment_item_detail, container, false);
        mTitleView = (TextView)v.findViewById(R.id.titleView);
        mSubtitleView = (TextView)v.findViewById(R.id.subtitleView);
        mReviewCountView = (TextView)v.findViewById(R.id.ratingCountView);
        mRatingView = (RatingBar)v.findViewById(R.id.ratingView);
        return v;
    }

    public void updateItem(Item item)
    {
        currentItem = item;

        mTitleView.setText(currentItem.getName());
        //ImageLoader loader = new ImageLoader(mImageView);
        //loader.execute(currentItem.getYelp_entry().getImage_url());
        mRatingView.setRating(currentItem.getYelp_entry().getRating());
        mSubtitleView.setText(PhoneNumberUtils.formatNumber(currentItem.getYelp_entry().getPhone(), "US"));
        mReviewCountView.setText(" - "+currentItem.getYelp_entry().getReview_count()+" reviews");

    }


}
