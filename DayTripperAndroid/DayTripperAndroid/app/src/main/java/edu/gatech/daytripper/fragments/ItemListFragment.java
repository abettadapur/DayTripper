package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.app.Fragment;
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
import edu.gatech.daytripper.adapters.ItemAdapter;
import edu.gatech.daytripper.model.Item;


/**
 * A fragment representing a list of Items.
 * <p/>
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnFragmentInteractionListener}
 * interface.
 */
public class ItemListFragment extends Fragment {



    private OnFragmentInteractionListener mListener;

    private List<Item> mItemList;
    private RecyclerView mReccyleView;
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
            mListener = (OnFragmentInteractionListener) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {
        View rootView = inflater.inflate(R.layout.fragment_item_list, container, false);
        mReccyleView = (RecyclerView)rootView.findViewById(R.id.recycle_view);

        mAdapter = new ItemAdapter(mItemList, getActivity());
        mReccyleView.setAdapter(mAdapter);

        mReccyleView.setLayoutManager(new LinearLayoutManager(getActivity()));
        mReccyleView.setItemAnimator(new DefaultItemAnimator());



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
