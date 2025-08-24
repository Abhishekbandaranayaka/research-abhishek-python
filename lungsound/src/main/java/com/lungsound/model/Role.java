package com.lungsound.model;

public enum Role {

    USER("ROLE_USER"),
    ADMIN("ROLE_ADMIN");

    private final String springRole;

    Role(String springRole){
        this.springRole = springRole;
    }

    public String getSpringRole() {
        return springRole;
    }
}
