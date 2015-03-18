package edu.gatech.daytripper.fragments;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;

import edu.gatech.daytripper.R;

/**
 * Created by Alex on 3/12/2015.
 */
public class CreateItineraryDialog extends DialogFragment
{
    private EditText mNameBox;
    private Spinner mCitySpinner;
    private ArrayAdapter<String> mCityAdapter;
    private final String[] cities = {"Atlanta", "New York City", "Seattle", "San Francisco", "Philadelphia"};

    public Dialog onCreateDialog(Bundle savedInstanceState)
    {
        AlertDialog.Builder b = new AlertDialog.Builder(getActivity())
                .setTitle("Create Itinerary")
                .setPositiveButton("Create", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //success
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        LayoutInflater i = getActivity().getLayoutInflater();
        View v = i.inflate(R.layout.dialog_create_itinerary, null);

        mNameBox = (EditText)v.findViewById(R.id.nameBox);
        mCitySpinner = (Spinner)v.findViewById(R.id.citySpinner);
        mCityAdapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_spinner_item, cities);
        mCitySpinner.setAdapter(mCityAdapter);

        ///View setup
        b.setView(v);
        return b.create();
    }

}
