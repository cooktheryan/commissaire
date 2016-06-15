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

@deploy
@cluster
Feature: Deploying Tree Image Across Clusters

  @anonymous
  Scenario: Initiate tree deployment without authentication
     Given we are anonymous
       and we have a cluster named honeynut
      when we initiate a tree deployment of cluster honeynut
      then commissaire will deny access

  Scenario: Initiate tree deployment with authentication
     Given we have a valid username and password
       and we have a cluster named honeynut
      when we initiate a tree deployment of cluster honeynut
      then commissaire will allow access
       and commissaire will note creation
       and commissaire will provide deployment status
       and the provided status is in_process
