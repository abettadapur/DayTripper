package edu.gatech.daytripper;

import android.app.Application;

import net.danlew.android.joda.JodaTimeAndroid;

/**
 * Created by Alex on 3/17/2015.
 */
public class DayTripperApplication extends Application
{
    @Override
    public void onCreate()
    {
        super.onCreate();
        JodaTimeAndroid.init(this);
    }
}
