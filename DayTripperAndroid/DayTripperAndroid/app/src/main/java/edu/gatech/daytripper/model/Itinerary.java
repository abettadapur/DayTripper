package edu.gatech.daytripper.model;

import com.google.gson.annotations.Expose;

import java.util.Calendar;
import java.util.List;

/**
 * Created by Alex on 3/7/2015.
 */
public class Itinerary implements Comparable<Itinerary>
{
    private int id;
    private String name;
    private Calendar date;
    private Calendar start_time;
    private Calendar end_time;
    private String city;
    @Expose(serialize = false)
    private List<Item> items;
    @Expose(serialize = false)
    private User user;


    public Itinerary(){}

    public Itinerary(String name, Calendar date, Calendar start_time, Calendar end_time, String city, List<Item> items)
    {
        this.id = 0;
        this.name = name;
        this.date = date;
        this.start_time = start_time;
        this.end_time = end_time;
        this.city = city;
        this.items = items;
    }

    public Itinerary(int id, String name, Calendar date, Calendar start_time, Calendar end_time, String city, List<Item> items)
    {

        this.id = id;
        this.name = name;
        this.date = date;
        this.start_time = start_time;
        this.end_time = end_time;
        this.city = city;
        this.items = items;
    }

    public List<Item> getItems() {
        return items;
    }

    public void setItems(List<Item> items) {
        this.items = items;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Calendar getDate() {
        return date;
    }

    public void setDate(Calendar date) {
        this.date = date;
    }

    public Calendar getStart_time() {
        return start_time;
    }

    public void setStart_time(Calendar start_time) {
        this.start_time = start_time;
    }

    public Calendar getEnd_time() {
        return end_time;
    }

    public void setEnd_time(Calendar end_time) {
        this.end_time = end_time;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public int compareTo(Itinerary another) {
        return this.getDate().compareTo(another.getDate());
    }
}
