package edu.gatech.daytripper.fragments;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.ProgressDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TimePicker;

import com.afollestad.materialdialogs.MaterialDialog;
import com.facebook.Session;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.model.Itinerary;
import edu.gatech.daytripper.net.RestClient;
import edu.gatech.daytripper.retro.interfaces.ItineraryService;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

/**
 * Created by Alex on 3/12/2015.
 */
public class CreateItineraryDialog extends DialogFragment
{
    private EditText mNameBox, mStartPicker, mEndPicker, mDatePicker, mCitySpinner;
    private Calendar mDate, mStart, mEnd;
    private ArrayAdapter<String> mCityAdapter;
    private final String[] cities = {"Atlanta", "Austin", "Miami", "Portland", "Philadelphia", "Seattle" };

    public Dialog onCreateDialog(Bundle savedInstanceState)
    {
        MaterialDialog.Builder b = new MaterialDialog.Builder(getActivity())
                .title("Create Itinerary")
                .positiveText("Create")
                .callback(new MaterialDialog.ButtonCallback() {
                    @Override
                    public void onPositive(MaterialDialog dialog) {
                        super.onPositive(dialog);
                        String name = mNameBox.getText().toString();
                        String city = mCitySpinner.getText().toString();

                        Itinerary newItinerary = new Itinerary(name, mDate, mStart, mEnd, city, new ArrayList<Item>());
                        ItineraryService service = new RestClient().getItineraryService();

                        final ProgressDialog progress  = ProgressDialog.show(CreateItineraryDialog.this.getActivity(), "Creating", "Creating a custom itinerary....", true);
                        service.createItinerary(newItinerary, Session.getActiveSession().getAccessToken(), new Callback<Itinerary>() {
                            @Override
                            public void success(Itinerary itinerary, Response response) {
                                progress.dismiss();
                                Log.e("CREATE ITINERARY", "SUCCESS "+response.getBody());
                                getTargetFragment().onActivityResult(getTargetRequestCode(), Activity.RESULT_OK, new Intent());
                            }

                            @Override
                            public void failure(RetrofitError error) {
                                progress.dismiss();
                                Log.e("CREATE ITINERARY", "FAIL: "+error.getMessage());
                            }
                        });
                    }

                    @Override
                    public void onNegative(MaterialDialog dialog) {
                        super.onNegative(dialog);
                        dialog.dismiss();
                    }
                })
                .negativeText("Cancel");


        LayoutInflater i = getActivity().getLayoutInflater();
        View v = i.inflate(R.layout.dialog_create_itinerary, null);

        mStart = Calendar.getInstance();
        mStart.set(Calendar.HOUR_OF_DAY, 10);
        mStart.set(Calendar.MINUTE, 0);

        mEnd = Calendar.getInstance();
        mEnd.set(Calendar.HOUR_OF_DAY, 21);
        mEnd.set(Calendar.MINUTE, 0);

        mDate = Calendar.getInstance();





        mNameBox = (EditText)v.findViewById(R.id.nameBox);
        mStartPicker = (EditText)v.findViewById(R.id.startPicker);
        mEndPicker = (EditText)v.findViewById(R.id.endPicker);
        mDatePicker = (EditText)v.findViewById(R.id.datePicker);

        mCitySpinner = (EditText)v.findViewById(R.id.citySpinner);


        mCitySpinner.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new MaterialDialog.Builder(getActivity())
                        .title("Cities")
                        .items(cities)
                        .itemsCallback(new MaterialDialog.ListCallback() {
                            @Override
                            public void onSelection(MaterialDialog dialog, View view, int which, CharSequence text) {
                                mCitySpinner.setText(cities[which]);
                            }
                        })
                        .positiveText(android.R.string.cancel)
                        .show();
            }
        });

        mStartPicker.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new TimePickerDialog(CreateItineraryDialog.this.getActivity(), startTimeSetListener, mStart.get(Calendar.HOUR), mStart.get(Calendar.MINUTE), true).show();
            }
        });

        mEndPicker.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new TimePickerDialog(CreateItineraryDialog.this.getActivity(), endTimeSetListener, mStart.get(Calendar.HOUR), mStart.get(Calendar.MINUTE), true).show();
            }
        });

        mDatePicker.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new DatePickerDialog(CreateItineraryDialog.this.getActivity(), dateSetListener, mDate.get(Calendar.YEAR), mDate.get(Calendar.MONTH), mDate.get(Calendar.DAY_OF_MONTH)).show();
            }
        });
        updateView();
        b.customView(v, false);
        return b.build();
    }

    DatePickerDialog.OnDateSetListener dateSetListener = new DatePickerDialog.OnDateSetListener() {
        @Override
        public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth) {
            mDate.set(Calendar.YEAR, year);
            mDate.set(Calendar.MONTH, monthOfYear);
            mDate.set(Calendar.DAY_OF_MONTH, dayOfMonth);
            updateView();
        }
    };

    TimePickerDialog.OnTimeSetListener startTimeSetListener = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
            mStart.set(Calendar.HOUR_OF_DAY, hourOfDay);
            mStart.set(Calendar.MINUTE, minute);
            updateView();
        }
    };

    TimePickerDialog.OnTimeSetListener endTimeSetListener = new TimePickerDialog.OnTimeSetListener() {
        @Override
        public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
            mEnd.set(Calendar.HOUR_OF_DAY, hourOfDay);
            mEnd.set(Calendar.MINUTE, minute);
            updateView();
        }
    };

    private void updateView()
    {
        String dateFormat = "MM/dd/yy";
        SimpleDateFormat dateSdf = new SimpleDateFormat(dateFormat, Locale.US);
        String timeFormat = "H:mm";
        SimpleDateFormat timeSdf = new SimpleDateFormat(timeFormat, Locale.US);

        mStartPicker.setText(timeSdf.format(mStart.getTime()));
        mEndPicker.setText(timeSdf.format(mEnd.getTime()));
        mDatePicker.setText(dateSdf.format(mDate.getTime()));
    }

}
