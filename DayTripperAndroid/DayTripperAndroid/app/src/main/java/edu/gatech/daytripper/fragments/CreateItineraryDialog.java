package edu.gatech.daytripper.fragments;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;

import edu.gatech.daytripper.R;

/**
 * Created by Alex on 3/12/2015.
 */
public class CreateItineraryDialog extends DialogFragment
{
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

        ///View setup
        b.setView(v);
        return b.create();
    }

}
