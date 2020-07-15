PUT /soil_index
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "properties" : {
            "hostname": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                  
                }
              }
            },
            "channel 0 Moisture Percentage" : { "type" : "long" },
            "channel 0 Sample": { "type" : "long" },
            "channel 1 Moisture Percentage" : { "type" : "long" },
            "channel 1 Sample": { "type" : "long" },
            "internal IP": { "type" : "ip" },
            "external IP": { "type" : "ip" },
            "timestamp": { "type" : "date" }
        }
    }
}
