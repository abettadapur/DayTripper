package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;

import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.ArrayList;
import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.activities.ItemDetailActivity;
import edu.gatech.daytripper.adapters.ItemAdapter;
import edu.gatech.daytripper.adapters.RecyclerItemClickListener;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.model.Itinerary;


/**
 * A fragment representing a list of Items.
 * <p/>
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnFragmentInteractionListener}
 * interface.
 */
public class ItemListFragment extends Fragment implements RecyclerItemClickListener.OnItemClickListener{



    private ItemListListener mListener;
    private List<Item> mItemList;
    private RecyclerView mRecycleView;
    private ItemAdapter mAdapter;


    public static ItemListFragment newInstance() {
        ItemListFragment fragment = new ItemListFragment();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public ItemListFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mItemList = new ArrayList<>();
    }


    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mListener = (ItemListListener)activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {
        View rootView = inflater.inflate(R.layout.fragment_item_list, container, false);
        mRecycleView = (RecyclerView)rootView.findViewById(R.id.recycle_view);

        mAdapter = new ItemAdapter(mItemList, getActivity());
        mRecycleView.setAdapter(mAdapter);

        mRecycleView.setLayoutManager(new LinearLayoutManager(getActivity()));
        mRecycleView.setItemAnimator(new DefaultItemAnimator());

        mRecycleView.addOnItemTouchListener(new RecyclerItemClickListener(getActivity(), this));



        return rootView;
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }





    public void updateItems(List<Item> items)
    {

        if(items!=null) {
            mItemList.clear();
            mItemList.addAll(items);
            mAdapter.notifyDataSetChanged();
        }
    }

    @Override
    public void onItemClick(View childView, int position) {
        int item_id = mItemList.get(position).getId();
        int itinerary_id = mListener.getItinerary().getId();

        Intent i = new Intent(getActivity(), ItemDetailActivity.class);
        i.putExtra(ItemDetailActivity.ITINERARY_ID_EXTRA, itinerary_id);
        i.putExtra(ItemDetailActivity.ITEM_ID_EXTRA, item_id);
        startActivity(i);
    }

    @Override
    public void onItemLongPress(View childView, int position) {

    }


    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface ItemListListener {
        // TODO: Update argument type and name
        public void refresh_list(ItemListFragment fragment);
        public Itinerary getItinerary();
    }

}
