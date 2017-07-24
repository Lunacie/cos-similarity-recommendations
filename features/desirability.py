
import math
import time
import datetime

from dataModule.database.db_segment import DbSegment
from list import DbList
from dataModule.database.dbConfig import segmentDb

from categories import CategoryList
from dataModule.features import FeatureList

class DesirabilityList(DbList) :

    _db = None
    _activities = []

    def __init__(self, activities) :
        super().__init__()
        self._activities = activities

        self.db = DbSegment()
        
        self.getLikesList(activities)
        self.getCheckoutList(activities)

        self.getDesirability(activities)
        
        self.db.close()
        #self.db.closeTunnel()


    def getDesirability(self, activities) :
        for activity in activities :
            likes = 0
            checkouts = 0
            
            if ("likes" in activity) :
                likes = activity['likes']
            if ('checkouts' in activity) :
                checkouts = activity['checkouts']

            activity['desirability'] = (likes + checkouts) / 2

    def getCheckoutList(self, activities) :

        print(segmentDb['db'])
        request = """
        select
        product_id
        , count(product_id) as checkout_starts
        --, anonymous_id -- Testing
        from """+ segmentDb['db']['schemaMobile'] +"""
        .checkout_started
        
        -- Can add a where clause to limit time frame
        
        GROUP BY product_id

        order BY checkout_starts desc;
        """
        print(request)    
        self._checkouts = self.db.execute(request)
        if (len(self._checkouts) < 1) :
            return None
        
        max = self._checkouts[0][1]
        if (max == 0) :
            return self._checkouts

        for activity in activities :
            for item in self._checkouts :
                if activity['publicId'] == item[0] :
                    activity['checkouts'] = (item[1] - 0) / (max - 0)
        return self._checkouts



    def getLikesList(self, activities) :
            
            request = """
            select
            a.product_id
            , count(a.product_id) as added_to_wishlist
            , count(r.product_id) as removed_from_wishlist
            -- , anonymous_id -- Testing
            
            FROM """+ segmentDb['db']['schemaMobile'] +"""
            .product_added_to_wishlist a
            -- Only products that have previously been added to the wishlist can be removed from it
            -- Exception: Added before tracking started (but error will converge to 0)
            LEFT JOIN """+ segmentDb['db']['schemaMobile'] +"""
            .product_removed_from_wishlist r
            on a.product_id = r.product_id
            
            GROUP BY a.product_id
            """
            print(request)
            self._likes = self.db.execute(request)
            if (len(self._likes) < 1):
                return None

            max = 0
            matches = []
            for item in self._likes :
                value = item[1] - item[2]
                if (value > max) :
                    max = value
                i = 0
                for current in activities :
                    if (item[0] == current['publicId']) :
                        current['likes'] = item[1] - item[2]
                        matches.append(i)
                    i += 1

                if max == 0 :
                    return self._likes
                
                x = 0
                nbMatches = len(matches)
                while (x < nbMatches) :
                    activities[matches[x]]['likes'] = (activities[matches[x]]['likes'] - 0) / (max - 0)
                    
                    x += 1
                    
                
            return self._likes



        
'''
        # Visitors who viewed this product, also viewed
            request = """
            select
            p.sku
            , count(p.sku) as views
            --, p.name -- Testing
            --, p.timestamp as other_view -- Testing
            --, u.timestamp as original_view -- Testing

            from """+ segmentDb['db']['schemaMobile'] +"""
            .product_viewed p
            
            right JOIN (
            select
            sku
            , anonymous_id
            , timestamp
            from """+ segmentDb['db']['schemaMobile'] +"""
            .product_viewed
            
            where sku = '""" + element['publicId'] + """') u
            on p.anonymous_id = u.anonymous_id
            
            WHERE
            p.sku != '""" + element['publicId'] + """' -- Excludes the product for which the query is executed
            -- Limit time frame to +/- 1 day
            and date_trunc('day', p.timestamp) >= date_trunc('day', u.timestamp - INTERVAL '1 day')
            and date_trunc('day', p.timestamp) <= date_trunc('day', u.timestamp  + INTERVAL '1 day')
            -- c) limit geography to a certain radius (need to query production database)
            -- d) Only return currently active products (need to query production database)
            
            GROUP BY  p.sku --, p.name
            
            order by views DESC; """
'''
