package com.rick.application.repository;

import com.rick.application.domains.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;



public interface CustomerRepository extends JpaRepository<Customer, Long> {

    @Query(value = "SELECT * FROM CUSTOMER WHERE customer_name LIKE %?1%",nativeQuery = true)
    List<Customer> findByNomeWith(@Param("name") String name);

    Customer findByCpf(String cpf);



}
