package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.app.DialogFragment;
import android.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.app.ListFragment;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
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
import edu.gatech.daytripper.adapters.RecyclerItemClickListener;
import edu.gatech.daytripper.model.Itinerary;

/**
 * A fragment representing a list of Items.
 * <p/>
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnFragmentInteractionListener}
 * interface.
 */
public class ItineraryListFragment extends Fragment implements RecyclerItemClickListener.OnItemClickListener, View.OnClickListener {


    private OnFragmentInteractionListener mListener;
    private List<Itinerary> mItineraryList;
    private FloatingActionButton mAddButton;
    private RecyclerView mRecycleView;
    private ItineraryAdapter mAdapter;
    private final int ITINERARY_CREATE_CODE = 86;

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
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {
        View rootView = inflater.inflate(R.layout.fragment_itinerary_list, container, false);
        mRecycleView = (RecyclerView)rootView.findViewById(R.id.recycle_view);

        mAdapter = new ItineraryAdapter(mItineraryList, getActivity());
        mRecycleView.setAdapter(mAdapter);

        mRecycleView.setLayoutManager(new LinearLayoutManager(this.getActivity()));
        mRecycleView.setItemAnimator(new DefaultItemAnimator());

        mRecycleView.addOnItemTouchListener(new RecyclerItemClickListener(getActivity(), this));

        mAddButton = (FloatingActionButton)rootView.findViewById(R.id.add_fab);
        mAddButton.attachToRecyclerView(mRecycleView);
        mAddButton.setOnClickListener(this);

        return rootView;
    }

    @Override
    public void onStart() {
        super.onStart();
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

    public void updateItems(List<Itinerary> items)
    {
        if(mItineraryList == null)
            mItineraryList = new ArrayList<>();

        mItineraryList.clear();
        mItineraryList.addAll(items);
        mAdapter.notifyDataSetChanged();
    }

    @Override
    public void onItemClick(View childView, int position)
    {
        int itinerary_id = mItineraryList.get(position).getId();
        Intent i = new Intent(getActivity(), ItineraryDetailActivity.class);
        i.putExtra("itinerary_id", itinerary_id);
        getActivity().startActivity(i);
    }

    @Override
    public void onItemLongPress(View childView, int position) {

    }

    /** Open a dialog to add a new itinerary. After collecting info, open edit itinerary activity **/
    @Override
    public void onClick(View v)
    {
        CreateItineraryDialog dialog = new CreateItineraryDialog();
        //dialog.setTargetFragment(this, ITINERARY_CREATE_CODE);
        dialog.show(getActivity().getFragmentManager(), "fm");

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
