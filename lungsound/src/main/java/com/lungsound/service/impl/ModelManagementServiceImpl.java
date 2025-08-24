package com.lungsound.service.impl;

import com.lungsound.service.ModelManagementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ModelManagementServiceImpl implements ModelManagementService {

    private RestTemplate restTemplate;

    private final String modelServiceUrl = "http://model-service:8001";

    @Override
    public void triggerModelRetrainning() {
        restTemplate.postForEntity(modelServiceUrl + "/retrain" , null , String.class);
    }

    @Override
    public String getModelMetrics() {
        ResponseEntity<String> response = restTemplate.getForEntity(modelServiceUrl + "/metrics" , String.class);
        return response.getBody();
    }
}
