package edu.gatech.daytripper.adapters;

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

import edu.gatech.daytripper.R;
import edu.gatech.daytripper.model.Item;
import edu.gatech.daytripper.model.Itinerary;

import static android.support.v7.widget.RecyclerView.Adapter;

/**
 * Created by Alex on 3/10/2015.
 */
public class ItemAdapter extends RecyclerView.Adapter<ItemAdapter.ViewHolder>
{
    public static class ViewHolder extends RecyclerView.ViewHolder
    {
        public TextView mTitleView;
        public TextView mSubtitleView;

        public ViewHolder(View itemView) {
            super(itemView);
            mTitleView = (TextView)itemView.findViewById(R.id.titleView);
            mSubtitleView = (TextView)itemView.findViewById(R.id.detailView);
        }
    }
    private List<Item> mItems;
    private Context mContext;

    public ItemAdapter(List<Item> items, Context context)
    {
        this.mItems = items;
        this.mContext=context;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.item_list_item, viewGroup, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(ViewHolder viewHolder, int i)
    {
        Item item = mItems.get(i);
        viewHolder.mTitleView.setText(item.getName());
        viewHolder.mSubtitleView.setText(item.getCategory());
    }

    @Override
    public int getItemCount() {
        return mItems==null ? 0: mItems.size();
    }
}
