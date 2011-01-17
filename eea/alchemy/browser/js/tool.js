(function(){

jQuery.EEAlchemyEvents = {
  Search: 'EEAlchemy-Search',
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
      var context = jQuery(self);
      var form = jQuery('form', context);

      jQuery('input[type=submit]', form).hide();
      jQuery('input[type=checkbox]', form).click(function(){
        self.options.validate(form);
      });

      form.submit(function(){
        jQuery('.submitting', context).removeClass('submitting');
        if(!self.valid){
          return false;
        }
        jQuery(document).trigger(jQuery.EEAlchemyEvents.Search, {form: form});
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
      jQuery(document).bind(jQuery.EEAlchemyEvents.Search, function(evt, data){
        self.options.search(data);
      });
    },

    search: function(data){
      var form = data.form;
      var query = form.serialize();
      var action = form.attr('action');
      jQuery(document).trigger(jQuery.EEAlchemyEvents.AjaxStart);
      jQuery.post(action, query, function(data){
        self.options.showResults(data);
        jQuery(document).trigger(jQuery.EEAlchemyEvents.AjaxStop);
      });
    },

    showResults: function(data){
      self.html(data);
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
