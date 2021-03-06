# Copyright (C) 2016  Red Hat, Inc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

@create
@hosts
Feature: Creating Hosts

  @anonymous
  Scenario: Creating a new host without authentication
     Given we are anonymous
      when we create the host 10.2.0.2
      then commissaire will deny access

  Scenario: Creating a new host with authentication
     Given we have a valid username and password
      when we create the host 10.2.0.2
      then commissaire will allow access
      and commissaire will note creation
      and commissaire will return the single host

  Scenario: Recreating a compatible host with authentication
     Given we have a valid username and password
       and a host already exists at 10.2.0.2
      when we create the host 10.2.0.2
      then commissaire will allow access
      and commissaire will note success

  Scenario: Recreating an incompatible host with authentication
     Given we have a valid username and password
      and a host already exists at 10.2.0.2
      and we set the key to bogus data
      when we create the host 10.2.0.2
      then commissaire will allow access
      and commissaire will note a conflict
