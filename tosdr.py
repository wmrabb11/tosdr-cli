#!/usr/bin/env python3

# DISCLAIMER: API provided by tosdr.org
# Source: https://tosdr.org/api/1/all.json

# @author: Will Rabb
# @date: 03/31/2020
# Python3 CLI to get Terms of Service data/ratings for a given Site

import argparse
import json

API_FILE = 'data/all.json'

def print_verbose(points):
    total_score = 0
    for p in points:
        title = p['title']
        desc = p['description']
        point = p['point']
        score = p['score']
        total_score += score
        print( f'[*] Title: {title}' )
        print( f'[*] Description: {desc}' )
        print( f'[*] Point: {point}' )
        print( f'[*] Score: {score}' )
        print( '--------------------' )
    print( f'[*] Total score: {total_score}' )

def print_summary(points):
    the_good = []
    the_bad = []
    the_ugly = []
    for p in points:
        title = p['title']
        if p['point'] == 'good':
            the_good.append( f'[+] {title}' )
        elif p['point'] == 'neutral':
            the_bad.append( f'[*] {title}' )
        elif p['point'] == 'bad':
            the_ugly.append( f'[-] {title}' )
    print( '--Positive--' )
    for g in the_good:
        print( g )
    print( '--Neutral--' )
    for b in the_bad:
        print( b )
    print( '--Negative--' )
    for u in the_ugly:
        print( u )

def find_close_match(site):
    json_file = open(API_FILE)
    data = json.load(json_file)
    for k, v in data.items():
        k.replace('tosdr/review/', '')
        if site in k and 'see' in v:
            return v['see']
        elif site in k:
            return k
    return None

def main(site, verbose=False, summary=False):
    print( f'-----Privacy Policy Info for {site}-----' )
    close_match = None
    with open(API_FILE) as json_file:
        data = None
        try:
            data = json.load(json_file)[f'tosdr/review/{site.lower()}']
            rating = data['rated']
            if verbose:
                points = data['points']
                print_verbose(points)
            elif summary:
                points = data['points']
                print_summary(points)
            print( '--Privacy Grade--' )
            if not rating:
                print( f'[-] {site} has not been rated yet' )
                return
            print( f'[*] Overall privacy rating: {rating}' )
        except Exception as e:
            close_match = find_close_match(site)
            print( f'[-] Data not found for {site}' )
            if close_match:
                print( f'[+] Did you mean \'{close_match}\'?' )
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Python3 CLI to analyze Privacy Policies for a given site")
    parser.add_argument('-s', '--site', help="Website to check the privacy policy for", required=True)
    parser.add_argument('-v', '--verbose', help="Indicates verbose output", action='store_true')
    parser.add_argument('-S', '--summary', help="Indicates Privacy Policty Summary", action='store_true')

    args = parser.parse_args()
    if args.site and args.verbose:
        main(args.site, verbose=True)
    elif args.site and args.summary:
        main(args.site, summary=True)
    elif args.site:
        main(args.site)
    else:
        parser.print_help()
