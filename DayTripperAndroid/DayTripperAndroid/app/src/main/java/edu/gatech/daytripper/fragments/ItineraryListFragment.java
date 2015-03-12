package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.app.ListFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.melnykov.fab.FloatingActionButton;

import java.util.ArrayList;
import java.util.List;

import edu.gatech.daytripper.R;

import edu.gatech.daytripper.activities.ItineraryDetailActivity;
import edu.gatech.daytripper.adapters.ItineraryAdapter;
import edu.gatech.daytripper.model.Itinerary;

/**
 * A fragment representing a list of Items.
 * <p/>
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnFragmentInteractionListener}
 * interface.
 */
public class ItineraryListFragment extends ListFragment {


    private OnFragmentInteractionListener mListener;
    private List<Itinerary> mItineraryList;
    private FloatingActionButton mAddButton;

    public static ItineraryListFragment newInstance() {
        ItineraryListFragment fragment = new ItineraryListFragment();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public ItineraryListFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mItineraryList = new ArrayList<>();
        // TODO: Change Adapter to display your content
        setListAdapter(new ItineraryAdapter(getActivity(), android.R.layout.simple_list_item_1, mItineraryList));



    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {
        return inflater.inflate(R.layout.fragment_itinerary_list, container, false);
    }

    @Override
    public void onStart() {
        super.onStart();
        mAddButton = (FloatingActionButton)getView().findViewById(R.id.add_fab);
        mAddButton.attachToListView(getListView());
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mListener = (OnFragmentInteractionListener) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }


    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);

        if (null != mListener) {
            // Notify the active callbacks interface (the activity, if the
            // fragment is attached to one) that an item has been selected.
           // mListener.onFragmentInteraction(DummyContent.ITEMS.get(position).id);
            int itinerary_id = mItineraryList.get(position).getId();
            Intent i = new Intent(getActivity(), ItineraryDetailActivity.class);
            i.putExtra("itinerary_id", itinerary_id);
            getActivity().startActivity(i);

        }
    }

    public void updateItems(List<Itinerary> items)
    {
        if(mItineraryList == null)
            mItineraryList = new ArrayList<>();

        mItineraryList.clear();
        mItineraryList.addAll(items);
        ((ItineraryAdapter)getListAdapter()).notifyDataSetChanged();
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
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        public void onFragmentInteraction(String id);
    }

}
