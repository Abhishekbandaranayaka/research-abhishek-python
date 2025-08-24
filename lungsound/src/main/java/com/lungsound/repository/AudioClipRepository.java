package com.lungsound.repository;

import com.lungsound.model.AudioClip;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AudioClipRepository extends JpaRepository<AudioClip , Long> {
}
