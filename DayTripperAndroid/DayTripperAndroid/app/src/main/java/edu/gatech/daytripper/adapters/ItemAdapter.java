package edu.gatech.daytripper.adapters;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.model.Itinerary;

/**
 * Created by Alex on 3/10/2015.
 */
public class ItemAdapter extends ArrayAdapter<Item>
{
    private List<Item> items;
    public ItemAdapter(Context context, int resource, List<Item> objects) {
        super(context, resource, objects);
        this.items = objects;
    }


    @Override
    public View getView(int position, View convertView, ViewGroup parent)
    {
        Item item = items.get(position);


        LayoutInflater mInflater = (LayoutInflater)getContext().getSystemService(Activity.LAYOUT_INFLATER_SERVICE);
        View view = mInflater.inflate(R.layout.item_list_item, null);

        TextView titleView = (TextView)view.findViewById(R.id.titleView);
        TextView detailView = (TextView)view.findViewById(R.id.detailView);

        titleView.setText(item.getName());


        return view;
    }
}
