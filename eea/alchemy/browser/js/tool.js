(function(){

jQuery.EEAlchemyEvents = {
  SearchStart: 'EEAlchemy-Search-Start',
  SearchStop: 'EEAlchemy-Search-Stop',
  AjaxStart: 'EEAlchemy-AJAX-Start',
  AjaxStop: 'EEAlchemy-AJAX-Stop',
  AjaxError: 'EEAlchemy-AJAX-Error'
};

/**

Search form
**/
jQuery.fn.EEAlchemySearch = function(settings){
  var self = this;
  self.valid = false;

  self.options = {
    initialize: function(){
      var form = jQuery('form', self);

      jQuery('input[type=submit]', form).hide();
      var img = jQuery('<img>')
        .attr('src', '++resource++eea.alchemy.loader.gif')
        .attr('id', 'eea-alchemy-loader')
        .css('display', 'inline')
        .hide();
      jQuery('input[type=submit]', form).after(img);

      jQuery('input[type=checkbox]', form).click(function(){
        self.options.validate(form);
      });

      // Events
      jQuery(document).bind(jQuery.EEAlchemyEvents.SearchStart, function(evt, data){
        self.options.search_start(form);
      });
      jQuery(document).bind(jQuery.EEAlchemyEvents.SearchStop, function(evt, data){
        self.options.search_end(form);
      });

      form.submit(function(){
        jQuery('.submitting', self).removeClass('submitting');
        if(!self.valid){
          return false;
        }
        jQuery(document).trigger(jQuery.EEAlchemyEvents.SearchStart, {form: form});
        return false;
      });
    },

    // Validate search form
    validate: function(form){
      self.valid = false;
      // Portal type required
      var portal_type = jQuery('input[name=portal_type]:checked', form).length;
      if(!portal_type){
        jQuery('input[type=submit]', form).hide();
        return false;
      }

      // Lookin required
      var lookin = jQuery('input[name=lookin]:checked', form).length;
      if(!lookin){
        jQuery('input[type=submit]', form).hide();
        return false;
      }

      // Discover required
      var discover = jQuery('input[name=discover]:checked', form).length;
      if(!discover){
        jQuery('input[type=submit]', form).hide();
        return false;
      }

      // Valid
      self.valid = true;
      jQuery('input[type=submit]', form).show();
    },

    search_start: function(form){
      jQuery('input[type=submit]', form).hide();
      jQuery('#eea-alchemy-loader').show();
    },

    search_end: function(form){
      jQuery('#eea-alchemy-loader').hide();
      jQuery('input[type=submit]', form).show();
    }
  };

  // Update settings
  if(settings){
    jQuery.extend(self.options, settings);
  }

  self.options.initialize();
  return this;
};

/**

Results
**/
jQuery.fn.EEAlchemyResults = function(settings){
  var self = this;

  self.options = {
    initialize: function(){
      // Bind events
      jQuery(document).bind(jQuery.EEAlchemyEvents.SearchStart, function(evt, data){
        self.options.search(data);
      });
    },

    search: function(data){
      var form = data.form;
      var query = form.serialize();
      var action = form.attr('action');
      jQuery(document).trigger(jQuery.EEAlchemyEvents.AjaxStart);
      jQuery.get(action, query, function(data){
        self.options.showResults(data);
        jQuery(document).trigger(jQuery.EEAlchemyEvents.AjaxStop);
        jQuery(document).trigger(jQuery.EEAlchemyEvents.SearchStop);
      });
    },

    showResults: function(data){
      self.html(data);
      var div = jQuery('<div>');
      var form = jQuery('form', self);
      form.after(div);
      div.EEAlchemyLoader();
    }
  };

  // Update settings
  if(settings){
    jQuery.extend(self.options, settings);
  }

  self.options.initialize();
  return this;
};

jQuery.fn.EEAlchemyLoader = function(settings){
  var self = this;
  self.addClass('alchemy-loader');

  self.options = {
    total: 100,
    current: 1,
    initialize: function(){
      self.bar = jQuery('<div>').addClass('alchemy-loader-bar');
      self.append(self.bar);
      self.options.update();
    },

    update: function(value){
      var total = self.options.total;
      if(value >= total){
        value = total;
      }

      self.options.current = value;
      var percent = value / total;
      self.bar.width(self.width() * percent);
    }
  };

  // Update settings
  if(settings){
    jQuery.extend(self.options, settings);
  }

  self.options.initialize();
  return this;
};
/**

Load
*/
jQuery(document).ready(function(){
  // Cleanup main template
  jQuery("#belowContent").remove();
  jQuery("#eea-comments").remove();
  jQuery(".discussion").remove();

  // Initialize
  jQuery('#eea-alchemy .alchemy-search').EEAlchemySearch();
  jQuery('#eea-alchemy .alchemy-results').EEAlchemyResults();
});

})();
