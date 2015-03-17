package edu.gatech.daytripper.model;

import com.google.gson.annotations.Expose;

import java.util.Date;

/**
 * Created by Alex on 3/7/2015.
 */
public class Item
{
    private int id;
    private String yelp_id;
    private String category;
    private String name;
    private Date start_time;
    private Date end_time;
    @Expose(serialize = false)
    private YelpEntry yelp_entry;

    public Item(int id, String yelp_id, String category, String name, Date start_time, Date end_time, YelpEntry yelp_entry) {
        this.id = id;
        this.yelp_id = yelp_id;
        this.category = category;
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.yelp_entry = yelp_entry;
    }

    public Item(int id, String yelp_id, String category, String name, Date start_time, Date end_time) {
        this.id = id;
        this.yelp_id = yelp_id;
        this.category = category;
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.yelp_entry = null;
    }

    public Item(String yelp_id, String category, String name, Date start_time, Date end_time) {
        this.yelp_id = yelp_id;
        this.category = category;
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.yelp_entry = null;
        this.id=-1;
    }

    public Item()  {}


    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getYelp_id() {
        return yelp_id;
    }

    public void setYelp_id(String yelp_id) {
        this.yelp_id = yelp_id;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Date getStart_time() {
        return start_time;
    }

    public void setStart_time(Date start_time) {
        this.start_time = start_time;
    }

    public Date getEnd_time() {
        return end_time;
    }

    public void setEnd_time(Date end_time) {
        this.end_time = end_time;
    }

    public YelpEntry getYelp_entry() {
        return yelp_entry;
    }

    public void setYelp_entry(YelpEntry yelp_entry) {
        this.yelp_entry = yelp_entry;
    }
}
