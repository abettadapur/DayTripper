//package edu.gatech.daytripper.activities;
//
//import android.app.Activity;
//import android.os.Bundle;
//import android.support.v4.widget.DrawerLayout;
//import android.support.v7.app.ActionBarActivity;
//import android.support.v7.app.ActionBarDrawerToggle;
//import android.view.View;
//import android.widget.AdapterView;
//import android.widget.ArrayAdapter;
//import android.widget.ListView;
//
//import java.util.Map;
//
//import edu.gatech.daytripper.R;
//
///**
// * Created by Alex on 3/25/2015.
// */
//public class DrawerActivity extends ActionBarActivity
//{
//    public DrawerLayout mDrawerLayout;
//    public ListView drawerList;
//    public String[] layers;
//    private ActionBarDrawerToggle drawerToggle;
//    private Map map;
//
//    protected void onCreateDrawer()
//    {
//        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
//
//        drawerToggle = new ActionBarDrawerToggle((Activity) this, mDrawerLayout, R.drawable.ic_drawer, 0)
//        {
//            public void onDrawerClosed(View view)
//            {
//
//            }
//
//            public void onDrawerOpened(View drawerView)
//            {
//                getActionBar().setTitle("Menu");
//            }
//        };
//
//        mDrawerLayout.setDrawerListener(drawerToggle);
//
//        layers = getResources().getStringArray(R.array.layers_array);
//        drawerList = (ListView)findViewById(R.id.left_drawer);
//        //View header = getLayoutInflater().inflate(R.layout.drawer_list_header, null);
//        //drawerList.addHeaderView(header, null, false);
//        drawerList.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, android.R.id.text1, layers));
//
//        drawerList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
//            @Override
//            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//                //something here
//            }
//        });
//
//    }
//
//}
